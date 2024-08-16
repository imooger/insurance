from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_app.models import get_db_connection
from flask_app.models.policy import Policy
from flask_app.models.client import Client
from flask_app.models.claim import Claim
from flask_app.models.statistics import Statistics
from flask_app.controllers.auth_controller import login_required, admin_required
from datetime import datetime, timedelta
from flask import abort

policy_bp = Blueprint("policy_bp", __name__)


@policy_bp.route("/policies")
@login_required
def policies():
    user_role = session["role"]
    user_email = session["email"]
    order_by = request.args.get("order_by", "end_date")
    order_dir = request.args.get("order_dir", "asc")
    reverse = (order_dir == "desc")
    current_year = datetime.now().year

    if user_role == "administrator":
        policies = [dict(policy) for policy in Policy.get_all_policies_for_admin()]
    elif user_role == "insured":
        policies = [dict(policy) for policy in Policy.get_policies_for_insured(user_email)]
    else:
        flash("Unauthorized access", "danger")
        return redirect(url_for("index"))

    for policy in policies:
        policy['total_premium'] = float(Client.get_premium_for_policy(policy['policy_id']))
    policies.sort(key=lambda x: x['total_premium'] if order_by == "total_premium" else x.get(order_by, ""), reverse=reverse)

    if user_role == "administrator":
        active_count = sum(1 for policy in policies if policy['activity'] == 'Active' and policy['status'] == 'Approved')
        expired_count = sum(1 for policy in policies if policy['activity'] == 'Expired' and policy['status'] == 'Approved')

        stats = {
            "current_year": current_year,
            "total_claim_amount": Statistics.get_total_claim_amount(),
            "house_policy_count": Statistics.get_active_policy_count_by_type("House"),
            "auto_policy_count": Statistics.get_active_policy_count_by_type("Auto"),
            "life_policy_count": Statistics.get_active_policy_count_by_type("Life"),
            "health_policy_count": Statistics.get_active_policy_count_by_type("Health"),
            "new_policies_count_by_month": Statistics.get_new_policies_count_by_month(),
            "active_policy_count": active_count,
            "expired_policy_count": expired_count,
        }

        return render_template("policies/policies.html", policies=policies, stats=stats, order_by=order_by, order_dir=order_dir, is_policy_ending_within_a_week=Client.is_policy_ending_within_a_week)

    return render_template("policies/policies.html", policies=policies, order_by=order_by, order_dir=order_dir, is_policy_ending_within_a_week=Client.is_policy_ending_within_a_week)



@policy_bp.route("/policy/<int:policy_id>", methods=["GET"])
@login_required
def policy_details(policy_id):
    policy = Policy.get_policy_by_id(policy_id)
    if not policy:
        abort(404, description="Policy not found")

    claims = Policy.get_claims_by_policy_id(policy_id)
    total_claims = Statistics.get_sum_of_claims_for_policy(policy_id)
    total_premium = round(Statistics.get_premium_for_policy(policy_id),2)
    loss_ratio = (total_claims / total_premium) * 100 if total_premium > 0 else 0

    return render_template('policies/policy_details.html', policy=policy, claims=claims, total_claims=total_claims, total_premium=total_premium, loss_ratio=loss_ratio)


@policy_bp.route("/add_policy", methods=("GET", "POST"))
@login_required
def add_policy():
    client_id = request.args.get("client_id", type=int)
    user_role = session["role"]

    today = datetime.today().date()
    next_year = today + timedelta(days=364)

    if request.method == "POST":
        form = request.form
        last_policy_id = Policy.get_last_policy_id() or 0
        policy_number = last_policy_id + 100000
        status = "Requested" if user_role == "insured" else "Approved"

        Policy.add_policy(
            client_id, policy_number, form["policy_type"], form["start_date"], form["end_date"], form["premium_amount"], status
        )
        
        return redirect(url_for("client_bp.client_details", client_id=client_id))
    return render_template("policies/add_policy.html", client_id=client_id, today=today, next_year=next_year)


@policy_bp.route("/edit_policy/<int:policy_id>", methods=("GET", "POST"))
@admin_required
def edit_policy(policy_id):
    policy = Policy.get_policy_by_id(policy_id)

    if policy is None:
        abort(404, description="Policy not found")
        

    if request.method == "POST":
        policy_number = request.form["policy_number"]
        policy_type = request.form["policy_type"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        premium_amount = request.form["premium_amount"]
        renewed = request.form.get("renewed", 0)
        status = request.form["status"]

        Policy.update_policy(
            policy_id, policy_number, policy_type, start_date, end_date, premium_amount,renewed,status
        )
        flash("Policy updated successfully", "success")
        #return back to the previous page
        next_url = request.form.get("next")
        return redirect(next_url or url_for("client_bp.client_details", client_id=policy["client_id"]))

    return render_template("policies/edit_policy.html", policy=policy)


@policy_bp.route("/delete_policy/<int:policy_id>/<int:client_id>", methods=["POST"])
@admin_required
def delete_policy(policy_id, client_id):
    try:
        # Fetch all claim IDs associated with the policy
        claim_ids = Claim.get_claims_by_policy(policy_id)
        for claim_id in claim_ids:
            Claim.delete_claim(claim_id)
        
        # Delete the policy
        Policy.delete_policy(policy_id)
        
        flash("Policy and associated claims deleted successfully", "warning")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
    
    return redirect(url_for("client_bp.client_details", client_id=client_id))

@policy_bp.route("/renew_policy/<int:policy_id>", methods=["POST"])
@admin_required
def renew_policy(policy_id):
    try:
        Policy.renew_policy(policy_id)
        flash("Policy renewed successfully", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(request.referrer or url_for("policy_bp.policies"))



