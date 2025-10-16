#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <ctime>
#include <curl/curl.h>
#include <cstdlib>

// Get current timestamp
std::string get_timestamp() {
    std::time_t now = std::time(nullptr);
    char buf[100];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
    return std::string(buf);
}

// Function to send POST request
void send_log(const std::string& url, const std::string& kerberos,
              int counter, const std::string& osname, const std::string& key) {
    CURL *curl = curl_easy_init();
    if (curl) {
        // Build JSON payload
        std::string json_data = R"({"kerberos":")" + kerberos +
                                R"(","counter":)" + std::to_string(counter) +
                                R"(,"osname":")" + osname +
                                R"(","key":")" + key + R"("})";

        struct curl_slist *headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data.c_str());
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L); // 10s timeout

        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK)
            std::cerr << "[" << get_timestamp() << "] Error: "
                      << curl_easy_strerror(res) << std::endl;
        else
            std::cout << "[" << get_timestamp() << "] Log sent successfully." << std::endl;

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
}

int main() {
    const std::string url = "http://10.17.5.8:8000/log/";
    const std::string osname = "Linux";

    curl_global_init(CURL_GLOBAL_ALL);

    while (true) {
        // Example usage: call function with dynamic/randomized values
        send_log(url, "agent-1", std::rand() % 100, osname, "XYZ123");

        // Wait 1 minute before next log
        std::this_thread::sleep_for(std::chrono::minutes(1));
    }

    curl_global_cleanup();
    return 0;
}