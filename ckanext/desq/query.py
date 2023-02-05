"""Database query utilities."""


def get_vocabulary_by_name(context, vocabulary_name):
    model = context['model']
    session = context['session']
    return session.query(model.Vocabulary).filter(
        model.Vocabulary.name == vocabulary_name
    ).first()
