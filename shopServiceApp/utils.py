# shopDashboardApp/utils.py (excerpt)

from shopServiceApp.signals import booking_changed

# your compute_and_broadcast_dashboard() from before...

booking_changed.connect(lambda sender, instance, created, deleted, **kw: compute_and_broadcast_dashboard())
