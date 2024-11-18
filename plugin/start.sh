#!/bin/bash
hypercorn src/QueryNiukePlugin:app --bind '0.0.0.0:8000' > plugin.log 2>&1 &