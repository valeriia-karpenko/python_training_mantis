# -*- coding: utf-8 -*-
import random

from model.project import Project


def test_del_project(app, db, check_ui):
    app.session.login("administrator", "root")
    if len(db.get_project_list()) == 0:
        app.project.create(Project(name="test"))
    old_projects = app.soap.get_project_list(username="administrator", password="root")
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.soap.get_project_list(username="administrator", password="root")
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    if check_ui:
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(),
                                                                     key=Project.id_or_max)