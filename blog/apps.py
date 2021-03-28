from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from django_comments.moderation import moderator
        from comments.moderation import CommentModerator
        moderator.register(self.get_model('Post'), CommentModerator)
        print(moderator._registry)
