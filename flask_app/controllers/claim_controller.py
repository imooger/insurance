from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_app.models import get_db_connection
from flask_app.controllers.auth_controller import login_required, admin_required
from flask_app.models.claim import Claim
from flask_app.models.statistics import Statistics
from datetime import datetime, timedelta

claim_bp = Blueprint("claim_bp", __name__)


@claim_bp.route("/claims")
@login_required
def claims():
    user_role = session["role"]
    user_email = session["email"]

    order_by = request.args.get("order_by", "claim_date")
    order_dir = request.args.get("order_dir", "asc")
    current_year = datetime.now().year

    if user_role == "administrator":
        claims = Claim.get_all_claims_for_admin(order_by=order_by, order_dir=order_dir)
        #print(len(claims))  # claims data passed to the template)
        #print(Statistics.get_claim_count_by_status("New"))
        stats = {
            "current_year": current_year,
            "claim_count_by_month": Statistics.get_claim_count_by_month(),
            "new_claim_count": Statistics.get_claim_count_by_status("New"),
            "pending_claim_count": Statistics.get_claim_count_by_status("Pending"),
            "paid_claim_count": Statistics.get_claim_count_by_status("Paid"),
            "denied_claim_count": Statistics.get_claim_count_by_status("Denied"),
            "house_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('House'),
            "auto_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('Auto'),
            "life_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('Life'),
            "health_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('Health')
        }
        return render_template("claims/claims.html", claims=claims, stats=stats, order_by=order_by, order_dir=order_dir)
    elif user_role == "insured":
        claims = Claim.get_claims_for_insured(user_email, order_by=order_by, order_dir=order_dir)
        #print(claims)  # claims data passed to the template
        return render_template("claims/claims.html", claims=claims, order_by=order_by, order_dir=order_dir)



@claim_bp.route("/claim", methods=["GET"])
@login_required
def claim_details():
    claim_id = request.args.get("claim_id", type=int)
    if claim_id is None:
        return apology("Claim ID is required", 400)

    claim = Claim.get_claim_by_id(claim_id)
    if not claim:
        return apology("Claim not found", 404)

    return render_template("claims/claim_details.html", claim=claim)


@claim_bp.route("/add_claim", methods=["GET", "POST"])
@login_required
def add_claim():
    policy_id = request.args.get("policy_id", type=int)
    today = datetime.today().date()

    if request.method == "POST":
        policy_id = policy_id  # request.form["policy_id"]
        description = request.form["description"]
        claim_amount = request.form["claim_amount"]
        claim_date = request.form["claim_date"]
        status = 'New' #request.form["status"]

        Claim.add_claim(policy_id, description, claim_amount, claim_date, status)

        return redirect(url_for("policy_bp.policy_details", policy_id=policy_id))

    return render_template("claims/add_claim.html", policy_id=policy_id, today=today)


@claim_bp.route("/edit_claim/<int:claim_id>", methods=["GET", "POST"])
@login_required
def edit_claim(claim_id):
    claim = Claim.get_claim_by_id(claim_id)
    user_role = session["role"]
    if not claim:
        return apology("Claim not found", 404)

    if request.method == "POST":
        description = request.form["description"]
        claim_amount = request.form["claim_amount"]
        claim_date = request.form["claim_date"]

        # Only admin can update status
        if user_role == "administrator":
            status = request.form["status"]
        else:
            status = claim["status"]  # Maintain current status if not admin


        Claim.update_claim(claim_id, description, claim_amount, claim_date, status)

        flash("Claim updated successfully", "success")
        next_url = request.form.get("next")
        return redirect(next_url or url_for("policy_bp.policy_details", policy_id=claim["policy_id"]))


    return render_template("claims/edit_claim.html", claim=claim,status_options=["New", "Pending", "Paid", "Denied"])


@claim_bp.route("/delete_claim/<int:claim_id>/<int:policy_id>", methods=["POST"])
@login_required
def delete_claim(claim_id, policy_id):
    Claim.delete_claim(claim_id)
    # Redirect to the previous page (referrer) if available, else to policy_details
    return redirect(
        request.referrer or url_for("policy_bp.policy_details", policy_id=policy_id)
    )
