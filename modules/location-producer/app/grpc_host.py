from concurrent import futures
import grpc
import location_pb2
import location_pb2_grpc
from kafka import KafkaProducer
import json

kafka_url = "udaconnect-kafka-0.udaconnect-kafka-headless.default.svc.cluster.local:9092"
kafka_topic = "udaconnect-locations"

# print("Connecting to kafka url: " + kafka_url)
# print("Sending kafka topics: " + kafka_topic)

kafka_producer = KafkaProducer(bootstrap_servers=kafka_url)
# print("Started KafkaProducer")
   
# GRPC endpoint to create locations
class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        request_value = {
            "person_id": int(request.person_id),
            "latitude": float(request.latitude),
            "longitude": float(request.longitude)
        }

        kafka_request = json.dumps(request_value).encode()
        kafka_producer.send(kafka_topic, kafka_request)
        kafka_producer.flush()
        return location_pb2.LocationMessage(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

location_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationServicer(), server
)

server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
