{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
{% if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_short_name }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_short_name }}

.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_short_name }}.svg
{%- endif %}


{{ cookiecutter.project_short_description }}

------------


Features
--------

* TODO


Usage
--------

* TODO
