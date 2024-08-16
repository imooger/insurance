from flask import Blueprint, render_template
from flask_app.models.statistics import Statistics
from flask_app.controllers.auth_controller import (
    login_required,
    admin_required,
    apology,
)

from datetime import datetime

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/stats")
@admin_required
def index():
    current_year = datetime.now().year
    
    stats = {
        "current_year": current_year,

        "client_count": Statistics.get_client_count(),
        "policy_count": Statistics.get_policy_count(),
        "new_claim_count": Statistics.get_new_claim_count(),
        "total_premium": Statistics.get_total_premiums(),
        "total_claim_amount": Statistics.get_total_claim_amount(),

        "house_policy_count": Statistics.get_active_policy_count_by_type("House"),
        "auto_policy_count": Statistics.get_active_policy_count_by_type("Auto"),
        "life_policy_count": Statistics.get_active_policy_count_by_type("Life"),
        "health_policy_count": Statistics.get_active_policy_count_by_type("Health"),

        "average_policies_per_client": Statistics.get_average_policies_per_client(),
        "average_premium_per_client": Statistics.get_average_premium_per_client(),
        "average_claims_per_client": Statistics.get_average_claims_per_client(),
        "average_claim_amount_per_client": Statistics.get_average_claim_amount_per_client(),
        "client_with_highest_claim": Statistics.get_client_with_highest_claim(),
        "client_with_highest_premium": Statistics.get_client_with_highest_premium(),
        "client_with_most_claims": Statistics.get_client_with_most_claims(),

        "claim_count_by_month": Statistics.get_claim_count_by_month(),
        "new_policies_count_by_month": Statistics.get_new_policies_count_by_month(),

        "all_claims_count_by_month": Statistics.get_all_claims_count_by_month(),
        "all_policies_count_by_month": Statistics.get_all_policies_count_by_month(),

        "new_claim_count": Statistics.get_claim_count_by_status("New"),
        "pending_claim_count": Statistics.get_claim_count_by_status("Pending"),
        "paid_claim_count": Statistics.get_claim_count_by_status("Paid"),
        "denied_claim_count": Statistics.get_claim_count_by_status("Denied"),

        "house_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('House'),
        "auto_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('Auto'),
        "life_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('Life'),
        "health_claim_count_by_policy_type": Statistics.get_claim_count_by_policy_type('Health'),


        "house_loss_ratio": Statistics.get_loss_ratio_by_policy_type('House'),
        "auto_loss_ratio": Statistics.get_loss_ratio_by_policy_type('Auto'),
        "life_loss_ratio": Statistics.get_loss_ratio_by_policy_type('Life'),
        "health_loss_ratio": Statistics.get_loss_ratio_by_policy_type('Health'),

        "paid_house_claim_by_type":Statistics.get_paid_claim_amount_by_type('House'),
        "paid_auto_claim_by_type":Statistics.get_paid_claim_amount_by_type('Auto'),
        "paid_life_claim_by_type":Statistics.get_paid_claim_amount_by_type('Life'),
        "paid_health_claim_by_type":Statistics.get_paid_claim_amount_by_type('Health'),

        "sum_of_house_by_type":Statistics.get_sum_of_earned_premiums_by_policy_type('House'),
        "sum_of_auto_by_type":Statistics.get_sum_of_earned_premiums_by_policy_type('Auto'),
        "sum_of_life_by_type":Statistics.get_sum_of_earned_premiums_by_policy_type('Life'),
        "sum_of_health_by_type":Statistics.get_sum_of_earned_premiums_by_policy_type('Health'),

        'house_claims_to_premiums_ratio': Statistics.get_claims_to_premiums_ratio('House'),
        'auto_claims_to_premiums_ratio': Statistics.get_claims_to_premiums_ratio('Auto'),
        'life_claims_to_premiums_ratio': Statistics.get_claims_to_premiums_ratio('Life'),
        'health_claims_to_premiums_ratio': Statistics.get_claims_to_premiums_ratio('Health'),

        'house_active_premiums': Statistics.get_active_policy_count_by_type('House'),
        'auto_active_premiums': Statistics.get_active_policy_count_by_type('Auto'),
        'life_active_premiums': Statistics.get_active_policy_count_by_type('Life'),
        'health_active_premiums': Statistics.get_active_policy_count_by_type('Health'),

        'house_expired_premiums': Statistics.get_expired_policy_count_by_type('House'),
        'auto_expired_premiums': Statistics.get_expired_policy_count_by_type('Auto'),
        'life_expired_premiums': Statistics.get_expired_policy_count_by_type('Life'),
        'health_expired_premiums': Statistics.get_expired_policy_count_by_type('Health'),


    }
    return render_template("stats/stats.html", stats=stats)
