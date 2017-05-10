from solrpy import core
s = core.SolrConnection('http://192.168.60.99:8983/solr/1_1472366655332')
response = s.query(q='*:*',fq='{!join from=id to=sqlid fromIndex=6 toIndex=1_1472366655332}( combined_all:(select \* from chentf.chentf_jdbc.stuinfo) )')
print(response.header['status'])
print(response.results.numFound)



