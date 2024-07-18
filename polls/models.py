from django.db import models


class Question(models.Model):

    question_txt = models.CharField(max_length=100)
    pub_date = models.DateTimeField('published date')

    def __str__(self):

        return (f'Question description : {self.question_txt}\n'
                f'Published date: {self.pub_date}')


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):

        return (f'Choice Description : {self.choice_text}\n'
                f'Votes Received : {self.votes}\n'
                f'Question to which choice is linked: {self.question}\n')



