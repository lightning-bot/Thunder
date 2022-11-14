from tortoise import fields
from tortoise.models import Model


class VoteBanCandidates(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.BigIntField()
    user_id = fields.BigIntField()

    voters: fields.ReverseRelation["VoteBanBallots"]

    class Meta:
        table = "voteban_candidates"


class VoteBanBallots(Model):
    ballot = fields.ForeignKeyField('models.VoteBanCandidates', related_name='voters', to_field="id")
    voter_id = fields.BigIntField()  # really it's the user's id

    class Meta:
        table = "voteban_ballots"
