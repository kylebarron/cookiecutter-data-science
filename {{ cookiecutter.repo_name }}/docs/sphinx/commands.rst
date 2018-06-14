Commands
========

The Makefile contains the central entry points for common tasks related to this project.

Syncing data to S3
^^^^^^^^^^^^^^^^^^

* `make sync` will use `rclone` to recursively sync files in the project folder to Dropbox. By default it doesn't sync the `.git` or the `data` folders.
