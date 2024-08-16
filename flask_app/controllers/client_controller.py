from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_app.models import get_db_connection
from flask_app.controllers.auth_controller import (
    login_required,
    admin_required,
    apology,
)
from flask_app.models.client import ClientManager, PolicyManager, ClaimsManager
from flask_app.models.claim import ClaimModification, ClaimRetrieval
from flask_app.models.statistics import Statistics
from flask_app.models.policy import PolicyService
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.models.auth import RegistrationService, UserService, AuthService
from datetime import date, datetime
import calendar

client_bp = Blueprint("client_bp", __name__)


@client_bp.route("/")
# @login_required
def index():
    # user_role = session["role"]
    # if user_role == "administrator":
    #     return redirect(url_for("dashboard_bp.index"))
    return render_template("welcome.html", show_user_info=False)

@client_bp.route("/in")
@login_required
def in_dex():
    user_role = session["role"]
    if user_role == "administrator":
        return redirect(url_for("dashboard_bp.index"))
    elif user_role == "insured":
        return redirect(url_for("client_bp.client_details"))
    return render_template("index.html", show_user_info=False)


@client_bp.route("/clients")
@admin_required
def clients():
    order_by = request.args.get("order_by", "first_name")
    order_dir = request.args.get("order_dir", "asc")

    clients = ClientManager.get_all_clients(order_by=order_by, order_dir=order_dir)
    
    clients_with_details = []
    for client in clients:
        client_dict = dict(client)
        
        # Fetch policies and categorize them
        client_policies = PolicyService.get_policies_by_client_id(client['client_id'])
        active_policies = [policy for policy in client_policies if policy['activity'] == 'Active']
        expired_policies = [policy for policy in client_policies if policy['activity'] == 'Expired']

        indv_total_premium = round(PolicyManager.get_sum_of_earned_premiums_by_client_id(client["client_id"]),2)
        
        # Fetch claims for the client
        claims = ClaimRetrieval.get_claims_for_client(client['client_id'])
        premium_per_month = round(PolicyManager.get_premium_per_month_on_active_policies(client["client_id"]),2)
        
        # Calculate sum of paid claims
        paid_claim_sum = sum([claim['claim_amount'] for claim in claims if claim['status'] == 'Paid'])

        # Add details to client_dict
        client_dict.update({
            'indv_total_premium': indv_total_premium,
            'premium_per_month': premium_per_month,
            
            'paid_claim_sum': paid_claim_sum,

            'active_policies': active_policies,
            'expired_policies': expired_policies,
            'claims': claims
        })
        
        clients_with_details.append(client_dict)

    # Sort clients based on the selected order_by and order_dir
    if order_by == 'paid_claim_sum':
        clients_with_details = sorted(clients_with_details, key=lambda x: x['paid_claim_sum'], reverse=(order_dir == 'desc'))
    else:
        clients_with_details = sorted(clients_with_details, key=lambda x: x[order_by], reverse=(order_dir == 'desc'))


    # Consolidate statistics
    stats = {
        "total_premium": Statistics.get_total_premiums(),
        "total_claim_amount": Statistics.get_total_claim_amount(),
        'house_active_premiums': Statistics.get_active_policy_count_by_type('House'),
        'auto_active_premiums': Statistics.get_active_policy_count_by_type('Auto'),
        'life_active_premiums': Statistics.get_active_policy_count_by_type('Life'),
        'health_active_premiums': Statistics.get_active_policy_count_by_type('Health'),
        'house_expired_premiums': Statistics.get_expired_policy_count_by_type('House'),
        'auto_expired_premiums': Statistics.get_expired_policy_count_by_type('Auto'),
        'life_expired_premiums': Statistics.get_expired_policy_count_by_type('Life'),
        'health_expired_premiums': Statistics.get_expired_policy_count_by_type('Health'),
        "new_claim_count": Statistics.get_claim_count_by_status("New"),
        "pending_claim_count": Statistics.get_claim_count_by_status("Pending"),
        "paid_claim_count": Statistics.get_claim_count_by_status("Paid"),
        "denied_claim_count": Statistics.get_claim_count_by_status("Denied"),
        "client_count": Statistics.get_client_count(),
        "policy_count": Statistics.get_policy_count(),
        "claim_count": Statistics.get_claim_count(),
    }
    
    return render_template("clients/clients.html", clients=clients_with_details, stats=stats, order_by=order_by, order_dir=order_dir)


@client_bp.route("/client", methods=["GET"])
@login_required
def client_details():
    user_role = session["role"]
    user_email = session["email"]

    if user_role == "administrator":
        client_id = request.args.get("client_id", type=int)
        if client_id is None:
            return apology("Client ID is required for administrators", 400)
        client = ClientManager.get_client_by_id(client_id)
    elif user_role == "insured":
        client = ClientManager.get_client_by_email(user_email)
    else:
        return apology("Unauthorized access", 403)

    if not client:
        return apology("Client not found", 404)


    policies = PolicyManager.get_policies_with_claim_counts(client["client_id"])
    indv_total_claims = ClaimsManager.get_total_claims_by_client_id(client["client_id"])
    indv_total_premium = round(PolicyManager.get_sum_of_earned_premiums_by_client_id(client["client_id"]),2)
    num_active_policies = PolicyManager.get_number_of_active_policies(client["client_id"])
    num_expired_policies = PolicyManager.get_number_of_expired_policies(client["client_id"])
    premium_per_month = round(PolicyManager.get_premium_per_month_on_active_policies(client["client_id"]),2)
    loss_ratio = (indv_total_claims / indv_total_premium) * 100 if indv_total_premium > 0 else 0

    # Calculate months active for each policy
    today = datetime.now().date()
    policies_with_details = []
    for policy in policies:
        policy_dict = dict(policy)
        try:
            start_date = datetime.strptime(policy_dict['start_date'], '%Y-%m-%d').date()
            end_date_str = policy_dict.get('end_date', None)
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                if start_date > end_date:
                    raise ValueError(f"Start date {start_date} is later than end date {end_date}.")
                if end_date > today:
                    end_date = today
            else:
                end_date = today

            months_active = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            policy_dict['months_active'] = 1 if months_active == 0 else months_active
            policy_dict['total_premium'] = PolicyManager.get_premium_for_policy(policy['policy_id'])
            policies_with_details.append(policy_dict)
        except ValueError as e:
            print(f"Error processing policy {policy['policy_id']}: {e}")


    return render_template(
        "clients/client_details.html",
        client=client,
        policies=policies_with_details,
        indv_total_claims=indv_total_claims,
        indv_total_premium=indv_total_premium,
        num_active_policies=num_active_policies,
        num_expired_policies=num_expired_policies,
        premium_per_month=premium_per_month,
        loss_ratio=loss_ratio,
        is_policy_ending_within_a_week=PolicyManager.is_policy_ending_within_a_week
    )


@client_bp.route("/add_client", methods=["GET", "POST"])
@login_required
def add_client():
    if session.get("role") != "administrator":
        return redirect(url_for("auth_bp.login"))

    if request.method == "POST":
        form_data = request.form.to_dict()
        form_data['photo'] = "https://i.pinimg.com/236x/c9/f7/d6/c9f7d650ce2a7f0f63ee7b1691694229.jpg"

        error, user_id = RegistrationService.register(
            form_data["email"],
            form_data["password"],
            form_data["first_name"],
            form_data["last_name"],
            form_data["date_of_birth"],
            form_data["phone"],
            form_data["street"],
            form_data["city"],
            form_data["state"],
            form_data["zip"],
            form_data["photo"],
            set_session=False,
        )

        if error:
            return apology(error, 400)

        flash("Client added successfully", "success")
        return redirect(url_for("client_bp.clients"))

    return render_template("clients/add_client.html", client_form=True)


@client_bp.route("/edit_client/<int:client_id>", methods=("GET", "POST"))
@login_required
def edit_client(client_id):
    client = ClientManager.get_client_by_id(client_id)
    
    # Fetch user info based on the client's email
    user = UserService.get_user_by_email(client['email'])
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        avatar_to_photo = {
            "female_1": "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-profiles/avatar-2.webp",
            "female_2": "https://mdbcdn.b-cdn.net/img/new/avatars/5.webp",
            "female_3": "https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(1).webp",
            "male_1": "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-profiles/avatar-1.webp",
            "male_2": "https://mdbcdn.b-cdn.net/img/new/avatars/1.webp",
            "male_3": "https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(9).webp",
            "bender_1": "https://i.pinimg.com/236x/ab/c8/6f/abc86f211ff6ca1f1f6ae5154f311bb5.jpg",
            "bender_2": "https://i.pinimg.com/236x/f1/df/26/f1df26cf3ab279c264c3645cd150c0f4.jpg",
            "bender_3": "https://i.pinimg.com/236x/c9/f7/d6/c9f7d650ce2a7f0f63ee7b1691694229.jpg",
            "leela_1": "https://i.pinimg.com/236x/8e/f9/d6/8ef9d6829121c7176a5192d9e97f6274.jpg",
            "fry_1": "https://i.pinimg.com/236x/c2/73/1d/c2731dea4191b182ecd8f18498562a84.jpg",
            "professor_1": "https://i.pinimg.com/236x/78/1d/80/781d806dcf7c0743b19b2a49b35b3869.jpg",
        }

        photo_link = avatar_to_photo.get(form_data.get("avatar"), client['photo'])
        form_data['photo_link'] = photo_link

        # Update the client in the Clients table
        ClientManager.update_client(
            client_id, 
            form_data["first_name"], 
            form_data["last_name"], 
            form_data["date_of_birth"], 
            form_data["email"], 
            form_data["phone"], 
            form_data["street"], 
            form_data["city"], 
            form_data["state"], 
            form_data["zip"], 
            form_data["photo_link"]
        )

        # Check if the email has changed and update it in the Users table
        if user and user['email'] != form_data["email"]:
            UserService.update_email(user['id'], form_data["email"])
            # Update the session email to match the new email
            session["email"] = form_data["email"]

        flash("Client updated successfully", "success")
        return redirect(form_data.get("next") or url_for("client_bp.client_details", client_id=client_id))

    return render_template("clients/edit_client.html", client=client)



@client_bp.route("/delete_client/<int:client_id>", methods=["POST"])
@admin_required
def delete_client(client_id):
    # Fetch the client's email before deleting the client
    client = ClientManager.get_client_by_id(client_id)
    if client:
        # Delete the user from the Users table
        UserService.delete_user_by_email(client['email'])
        
        # Delete the client from the Clients table
        ClientManager.delete_client(client_id)

    # Redirect to a known route, such as the clients list
    return redirect(url_for("client_bp.clients"))