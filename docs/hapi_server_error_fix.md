Ugh, bummer—nothing's wrong with your query. That 500/HAPI-0389 is coming straight from the demo server's JPA layer, which means the public test instance's database is trashed or unreachable. It happens more than you'd think on that "not for production" box.

**What you can do:**

1. **Wait or ping the HAPI team for a restart.**  
   The fix is usually "just restart the container" on the server side. Folks in the HAPI chat (chat.fhir.org, stream **#hapi**) can bump it for you .

2. **Switch to the R5 endpoint.**  
   If you don't strictly need R4 data, try  

   ```
   GET https://hapi.fhir.org/baseR5/Patient?_count=5
   ```  

   It's a separate instance and might be healthy.

3. **Run your own local HAPI JPA server.**  
   Spinning up the Docker image gives you full control and zero downtime.

Sorry you hit this—your query's legit. The demo server's just being flaky. Let me know if you want help bootstrapping a local instance!

---

### Pull & run the HAPI JPA server

```sh
docker pull hapiproject/hapi:latest  
docker run -d \
  --name myhapi \
  -p 8080:8080 \
  hapiproject/hapi:latest
```

### Check it

```sh
docker logs -f myhapi
curl -I http://localhost:8080/fhir
```

### Verify the endpoint

```sh
curl -s "http://localhost:8080/fhir/Patient?_count=1"
```

<br>
