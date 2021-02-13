import time

from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_name("Add Project")) > 0):
            wd.get("http://localhost/mantisbt-1.2.20/manage_proj_page.php")

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        # init project creation
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        # fill project form
        self.fill_project_form(project)
        # submit project creation
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        # wd.switch_to_alert().accept()
        time.sleep(3)
        self.project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            for element in wd.find_elements_by_css_selector("span.group"):
                text = element.text
                id = element.find_element_by_name("selected[]").get_attribute("value")
                self.project_cache.append(Project(name=text, id=id))

        return list(self.project_cache)

    def count(self):
        wd = self.app.wd
        self.app.open_projects_page()
        return len(wd.find_elements_by_name("selected[]"))

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector(f'a[href ^= "manage_proj_edit_page.php?project_id={str(id)}"]').click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        # select group
        self.select_project_by_id(id)
        # submit deletion
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_cache = None
