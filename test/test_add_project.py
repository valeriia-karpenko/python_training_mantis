from model.project import Project


def test_add_project(app, db, json_projects, check_ui):
    app.session.login("administrator", "root")
    project = json_projects
    old_projects = app.soap.get_project_list(username="administrator", password="root")
    app.project.create(project)
    new_projects = app.soap.get_project_list(username="administrator", password="root")
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    if check_ui:
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(),
                                                                     key=Project.id_or_max)