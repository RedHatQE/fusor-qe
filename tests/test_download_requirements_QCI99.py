# QCI-99

# On the "Select products to deploy" screen, the link to download the
# requirements works and contains relevant data.

from urllib2 import urlopen

def test_download_requirements(home_page_logged_in, base_url, expected_text):
    url = base_url.replace("https", "http")
    if url[-1] == "/":
        url = url[:-1]
    link = "{}/fusor_ui/files/QCI_Requirements.txt".format(url)
    data = urlopen(link).read()

    assert data == expected_text['requirements_file']
