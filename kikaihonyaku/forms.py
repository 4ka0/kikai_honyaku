from django import forms


CHOICES = [("Ja>En", "Japanese to English"), ("En>Ja", "English to Japanese")]


class SourceTextInputForm(forms.Form):

    # Radio buttons for the translation direction
    direction = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        initial="Ja>En",
        label=False,
        required=True,
    )

    # Text area for inputting the source text to be translated
    source_text = forms.CharField(
        widget=forms.Textarea, required=True, label=False
    )
