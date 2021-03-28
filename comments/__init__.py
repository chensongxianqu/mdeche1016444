def get_model():
    from .models import MyComment
    return MyComment


def get_form():
    from .forms import MyCommentForm
    return MyCommentForm
