from __future__ import print_function
from flask import Flask, render_template, g, request, session, redirect, url_for, abort, flash, jsonify
import os, sys, string
import sqlite3
from contextlib import closing
from werkzeug.debug import DebuggedApplication

conn = sqlite3.connect('clinical.sqlite')
c = conn.cursor()

q = 'select * from combo where problem_names like "' + '%' + 'lung cancer' +'%" or problem_names like "' + '%' + 'smok' +'%" or problem_names like "%nicotine%" or problem_names like "' + '%' + 'cigarette%" or problem_names like "%tobacco%";'
print(q, file = sys.stderr)
print("\n", file = sys.stderr)
c.execute(q)
data = [dict((c.description[idx][0], value)
       for idx, value in enumerate(row)) for row in c.fetchall()]
print("\n", file = sys.stderr)
print(data, file = sys.stderr)