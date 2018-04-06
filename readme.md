# Browser cookie whitelist pruner

This script removes all cookies from Firefox browser cache that are
not coming from the given whitelist.

To use, create a file called `preserved_host_suffixes.txt` with the
list of hosts you want preserved, one per line. Like this:

    your_chat_website.com
    work_email_site.com

Then shut down Firefox and run the script:

    ./prune_cookies.py

After this every cookie whose hostname does not end with an entry in
the file is deleted. This means that, for example, cookies from
`foo.your_chat_server.com` are preserved, but those from `foobar.com`
are deleted.
