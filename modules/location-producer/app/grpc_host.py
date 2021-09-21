from concurrent import futures
import json
import os
import time
from kafka import KafkaProducer
import grpc
import location_pb2
import location_pb2_grpc

kafka_url = "udaconnect-kafka-0.udaconnect-kafka-headless.default.svc.cluster.local:9092"
kafka_topic = "udaconnect-locations"

print("Connecting to kafka url: " + kafka_url)
print("Sending kafka topics: " + kafka_topic)

kafka_producer = KafkaProducer(bootstrap_servers=kafka_url)
print("Started KafkaProducer")
   
# GRPC endpoint to create locations
class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        request_value = {
            'person_id': int(request.person_id),
            'longitude': float(request.longitude),
            'latitude': float(request.latitude)
        }

        print('processing request ' + request)
                
        kafka_data = json.dumps(request_value).encode()
        kafka_producer.send(kafka_topic, kafka_data)
        kafka_producer.flush()
        return location_pb2.LocationMessage(**request_value)

# TODO: Start GRPC server only once KAFKA is ready.
time.sleep(15)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)