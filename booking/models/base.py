from django.db import models
import cuid2


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_id(cls):
        if not cls.id_prefix:
            raise NotImplementedError(
                "Derived models must specify id_prefix in Meta class"
            )
        return f"{cls.id_prefix}_{cuid2.Cuid().generate()}"

    def generate_id(self):
        return self.__class__.get_id()

    id = models.CharField(primary_key=True, max_length=255, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
