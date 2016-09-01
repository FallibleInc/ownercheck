### Ownercheck

`ownercheck` can be used to verify ownership of domains and mobile apps hosted on Android Play store or iOS app store. Domains can be verified by either adding a DNS record (CNAME or a TXT record) or by adding content to the existing website(a meta tag or uploading an empty file with the specified name). Mobile apps can be verified by checking the corresponding app page on app store for mention of user's verified domain in developers section of the page. 

The library used SQLite to store and match generated verification codes, which can be easily swapped with any database backend you use (check db.py, will make it configurable later).

#### Installation

``` bash
pip install ownercheck
````

#### Running tests

````
pip install tox 
tox
```


#### How to use

##### Verify domain ownership

###### User has access to the domain DNS settings

``` python
import ownercheck

ownercheck.generate_code('example.com', 'CNAME') 
# Now proceed to add a DNS entry for CNAME
ownercheck.verify_domain('example.com', 'CNAME')
```

###### User has access to the content hosted on the domain

``` python
import ownercheck

ownercheck.generate_code('example.com', 'METATAG') # Now proceed to add meta tag in your index.html as directed
ownercheck.verify_domain('example.com', 'CNAME') # returns a bool
```


##### Fetch mobile app links from domain

``` python
import ownercheck

ownercheck.fetch_apps(domain) # Do not use this for mobile apps verification. A malacious user can link to apps they do not own.
```


##### Verify ownership of mobile apps on Play/App Store 

``` python
import ownercheck

app_url = '' # Your Play store or App store published app URL    
domain = '' # Your domain related to the app    

ownercheck.verify_app(app_url, domain)
```

