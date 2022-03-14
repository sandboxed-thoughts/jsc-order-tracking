from django.db import models


class Gravel(BaseOrder):
    """A Django model for Gravel Orders

    Fields:
        caller (str): the person that called and placed the order
        bsdt (str): a string value representing the choices b/s and d/t
        priority (str): the urgency of the order
        rloads (int): the requested amount of gravel in loads
        dloads (int): the loads amount of gravel in loads
        ndate (date): the date the order is needed
        ddate (date): the date the order was delivered
        supplier (int): the pk of the Supplier instance responsible for providing the ordered gravel
        stype (str): the type of gravel orderd
        driver (str): the person responsible for delivering the order

    Managers:
        objects : The base manager from Django
        complete : A manager returning only objects where is_complete is True
        noncomplete : A manager returning only objects where is_complete is False
    """

    # choices
    class BSDT:
        B = "B/S"
        D = "D/T"
        choices = [
            (B, "B/S"),
            (D, "D/T"),
        ]

    # fields
    job_site = models.ForeignKey(
        "jobs.JobSite", verbose_name=_("Subdivision"), related_name="gravel_orders", on_delete=models.CASCADE
    )
    caller = models.CharField(_("Caller"), max_length=50)
    bsdt = models.CharField(_("B/S D/T"), max_length=3, choices=BSDT.choices, default=BSDT.B)
    priority = models.CharField(_("Priority"), max_length=50)
    rloads = models.PositiveIntegerField(
        _("Loads Requested"),
    )
    dloads = models.PositiveIntegerField(
        _("Loads Delivered"),
    )
    ndate = models.DateField(_("Date Needed"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ddate = models.DateField(_("Delivery / Pour Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    supplier = models.ForeignKey(
        "suppliers.Supplier", verbose_name="supplier", related_name="gravel_orders", on_delete=models.PROTECT
    )
    stype = models.ForeignKey(
        "suppliers.StoneType", verbose_name="stone type", related_name="orders", on_delete=models.PROTECT
    )
    driver = models.CharField(_("Driver"), max_length=25, blank=True, null=True)
    history = HR(inherit=True)

    # querysets from managers
    objects = models.Manager()
    complete = CompleteOrderManager()
    in_progress = NonCompleteOrderManager()

    def __str__(self) -> str:
        return "Order: {0} - Site: {1}".format(self.po, self.job_site)

    def save(self, *args, **kwargs):
        if any[
            (self.rloads == self.dloads),
            (self.progress == "complete"),
        ]:
            self.is_complete = True
        super(Gravel, self).save(*args, **kwargs)

    class Meta:
        db_table = "g_orders"
        managed = True
        verbose_name = "Gravel Order"
        verbose_name_plural = "Gravel Orders"
