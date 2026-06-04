from sqlalchemy import Column, Boolean

class SoftDeleteMixin:
    def soft_delete(self):
        if hasattr(self, "is_deleted"):
            self.is_deleted = True

        if hasattr(self, "is_active"):
            self.is_active = False
