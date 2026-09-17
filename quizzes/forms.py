from django import forms


class QuizSubmitForm(forms.Form):
    """Dinamik ravishda quiz savollari uchun form yaratadi."""

    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in questions:
            choices = [
                (answer.pk, answer.text)
                for answer in question.answers.all()
            ]
            self.fields[f'question_{question.pk}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
                error_messages={'required': 'Iltimos, javobni tanlang.'}
            )

    def get_answer_for_question(self, question_id):
        return self.cleaned_data.get(f'question_{question_id}')
