# import the stuff we need for web requests
import urequests
import ujson
from config import TOKEN, UBIDOTS_BASE_URL, DEVICE_LABEL, VARIABLE_LABEL, VARIABLE_LABEL_2

# class to handle sending data to ubidots
class UbidotsClient:
    def __init__(self):
        # make the url for sending data
        self.ubidots_variable_values_url = UBIDOTS_BASE_URL + DEVICE_LABEL + "/" + VARIABLE_LABEL + "/values"
        # headers for the request
        self.headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        # try to warm up the connection
        self._warm_up_connection()

    def _warm_up_connection(self):
        try:
            print("Sending initial value to Ubidots...")
            # send actual value 0 as the first request to warm up connection
            response = self.send_data_to_cloud(0, timeout=10, retries=2)
            if response:
                print("Initial value sent successfully - connection ready")
            else:
                print("Initial value failed - will retry on actual requests")
        except Exception as e:
            print(f"Initial value send failed (non-critical): {e}")

    def send_data_to_cloud(self, value, timeout=10, retries=2):
        # make the data to send
        data_to_send = {
            'value': value,
        }
        json_string = ujson.dumps(data_to_send)
        json_bytes = json_string.encode('utf-8')

        print(f"Attempting to send: {json_string} to {self.ubidots_variable_values_url}")

        # try multiple times if it fails
        for attempt in range(retries + 1):
            response = None
            try:
                print(f"Request attempt {attempt + 1}/{retries + 1}")
                # send the post request
                response = urequests.post(
                    self.ubidots_variable_values_url,
                    headers=self.headers,
                    data=json_bytes,
                    timeout=timeout
                )
                print(f"Ubidots API Response Status: {response.status_code}")
                print(f"Ubidots API Response Text: {response.text}")
                return response
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries:
                    print(f"Retrying in 1 second...")
                    from utime import sleep
                    sleep(1)
                else:
                    print(f"All {retries + 1} attempts failed")
                    return None
            finally:
                # always close the response
                if response:
                    response.close()

    def send_distance_data(self, distance, timeout=10, retries=2):
        # make the data to send
        data_to_send = {
            'value': distance,
        }
        json_string = ujson.dumps(data_to_send)
        json_bytes = json_string.encode('utf-8')

        distance_url = UBIDOTS_BASE_URL + DEVICE_LABEL + "/" + VARIABLE_LABEL_2 + "/values"
        print(f"Attempting to send distance: {json_string} to {distance_url}")

        # try multiple times if it fails
        for attempt in range(retries + 1):
            response = None
            try:
                print(f"Distance request attempt {attempt + 1}/{retries + 1}")
                # send the post request
                response = urequests.post(
                    distance_url,
                    headers=self.headers,
                    data=json_bytes,
                    timeout=timeout
                )
                print(f"Distance API Response Status: {response.status_code}")
                print(f"Distance API Response Text: {response.text}")
                return response
            except Exception as e:
                print(f"Distance attempt {attempt + 1} failed: {e}")
                if attempt < retries:
                    print(f"Retrying distance send in 1 second...")
                    from utime import sleep
                    sleep(1)
                else:
                    print(f"All {retries + 1} distance attempts failed")
                    return None
            finally:
                # always close the response
                if response:
                    response.close()

    # simple function to send data
    def send_data(self, value):
        return self.send_data_to_cloud(value)

    def send_distance(self, value):
        return self.send_distance_data(value)
