#!/bin/bash

# This script demonstrates using symmetric GPG non-interactively,
# suitable for an automated process.  This is intrinsically risky,
# because the passphrases must be passed around somehow.  However, it
# may be a necessary step sometimes.  Adapt this to your needs and
# adapt as necessary.  The biggest risk is that *all* command line
# arguments are, by default, visible to *all* users on a system.  This
# script is made to use only bash builtins to prevent this, and also
# pass it to gpg securely.
#
# If run as a script, it will prompt for a password and encrypt each
# file given on the commandline.
#
# - *always* make sure that you test you can decrypt files after using
#   this!
# - If using interactively, beware the risk of making a password
#   mistake and making your files inaccessible
# - If password is in a file, beware of the risks of that file ending
#   up handled insecurely, being backed up, etc.



# Simple option, if key is in a file.  Make sure file doesn't have
# extra spaces or newlines, even after the password!
# gpg --batch --symmetric --passphrase-file < /some/password_file.txt



# Actual interactive part.

read -s -p "Enter password: " password1
echo
read -s -p "Verify password: " password2
echo

if [[ "$password1" != "$password2" ]] ; then
    echo "Passwords do not match"
    exit 2
fi

# Loop through each file and encrypt.
for file in $@ ; do
    gpg --batch --symmetric --passphrase-file <( echo "$password1" ) $file
done

