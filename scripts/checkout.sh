#!/bin/sh

DEST="/var/www"
REPOSITORY="git://github.com/jpgneves/hojehatransportes.git"

mkdir -p "$DEST"
cd "$DEST"
git clone "$REPOSITORY"
