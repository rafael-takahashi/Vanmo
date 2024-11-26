#!/bin/bash
CD backend
uvicorn main:app --reload
read -p "Aperte enter para continuar . . . "