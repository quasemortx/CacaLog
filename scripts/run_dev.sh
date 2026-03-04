#!/bin/bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > uvicorn_debug.log 2>&1
