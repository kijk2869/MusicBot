from tortoise import fields, models


class Guild(models.Model):
    id = fields.BigIntField(pk=True, description="discord guild id")

    class Meta:
        table = "guilds"
        table_description = "Table of guild datas"

    def __int__(self):
        return self.id

    def __repr__(self):
        return f"<Guild" + f" id={self.id}" + ">"
