# CodeReviewAI

## run
```shell
bash ./dc.sh up
```

## test
```shell
bash ./scripts/test.sh
```


To process a large number of requests, I would use Kafka or Rabbit to add tasks to the queue, run programs on different servers or configure them to listen to this queue through multiprocessing

When processing large data stores, we can break them into smaller parts, and then draw a general conclusion based on the results

With GitHub, the problem of the number of requests can be solved by adding a VPN

To summarize, caching, using queues, using different models, using proxies