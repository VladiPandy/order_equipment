from django import forms
from .models import OpenWindowForOrdering
from .models import _gen_start_date_choices, get_week_period_choices, _get_week_period_choices

class OpenWindowForOrderingAdminForm(forms.ModelForm):
    class Meta:
        model  = OpenWindowForOrdering
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- динамический список дат ---
        start_choices = _gen_start_date_choices()
        if self.instance.pk:
            cur = self.instance.start_date
            if (cur, cur) not in start_choices:
                start_choices.append((cur, cur))
        self.fields["start_date"].choices = start_choices

        # --- динамический список недель ---
        week_choices = _get_week_period_choices()
        if self.instance.pk:
            cur = self.instance.week_period
            if (cur, cur) not in week_choices:
                week_choices.append((cur, cur))
        self.fields["week_period"].choices = week_choices