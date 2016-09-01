### Ownercheck

`ownercheck` can be used to verify ownership of domains and mobile apps hosted on Android Play store or iOS app store.

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

###### You have access to the domain DNS settings

``` python
import ownercheck

ownercheck.generate_code('http://example.com', 'CNAME') # Now proceed to add a DNS entry for CNAME
ownercheck.verify_domain('http://example.com', 'CNAME')
```

###### You have access to the content hosted on the domain

``` python
import ownercheck

ownercheck.generate_code('example.com', 'METATAG') # Now proceed to add meta tag in your index.html as directed
ownercheck.verify_domain('example.com', 'CNAME') # returns a bool
```

##### Verify mobile apps ownership

``` python
import ownercheck

app_url = '' # Your Play store or App store published app URL    
domain = '' # Your domain related to the app    

ownercheck.verify_app(app_url, domain)
```

##### Fetch mobile app links from domain

``` python
import ownercheck

ownercheck.fetch_apps(domain) # Do not use this for mobile apps verification. A malacious user can link to apps they do not own.
```


