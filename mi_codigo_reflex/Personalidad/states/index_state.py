import reflex as rx
from Personalidad.api.index_api import user, changePassword

class RadixFormSubmissionState(rx.State):
    form_data: dict
    click_count: int = 0

    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        
        await user(self.form_data["email"])
        

    @rx.var
    def form_data_keys(self) -> list:
        return list(self.form_data.keys())

    @rx.var
    def form_data_values(self) -> list:
        return list(self.form_data.values())