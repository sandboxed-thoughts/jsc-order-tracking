from django.contrib.admin import SimpleListFilter
from django.utils import timezone


class OverdueFilter(SimpleListFilter):
    title = "Order Overdue"
    parameter_name = "is_overdue"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples.

        The first element in each tuple is the coded value for the option that will appear in the URL query.
        The second element is the human-readable name for the option that will appear in the right sidebar.
        """
        return (
            ("True", "yes"),
            ("False", "no"),
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the value provided in the query string

        Retrievable via `self.value()`.
        """
        if self.value() == "True":
            return queryset.filter(ndate__lte=timezone.now())

        if self.value() == "False":
            return queryset.filter(ndate__gte=timezone.now())
        
        return queryset
