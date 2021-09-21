import grpc
import location_pb2
import location_pb2_grpc


# Simulates sending of coordinates from e.g. a mobile device
print("Sending coordinates")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
user_location_1 = location_pb2.LocationMessage(
    person_id=1,
    latitude=25.0707,
    longitude=15.4395
)

user_location_2 = location_pb2.LocationMessage(
    person_id=2,
    latitude=35.7749,
    longitude=122.4194
)

response1 = stub.Create(user_location_1)
response2 = stub.Create(user_location_2)

print("Coordinates sent...")
print(user_location_1, user_location_2)