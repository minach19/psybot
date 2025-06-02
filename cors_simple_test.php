<?php
// This is a simple file to test CORS headers - now with dynamic origin handling

// Get the origin from the request
$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';

// List of allowed origins - add more as needed
$allowed_origins = array(
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost',
    'http://127.0.0.1',
    'null'  // For local file access
);

// Set the CORS headers based on origin
if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
} else {
    // If origin is not in allowed list, use wildcard
    header("Access-Control-Allow-Origin: *");
}

// Additional CORS headers
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
header("Access-Control-Allow-Credentials: true");
header("Access-Control-Max-Age: 86400");  // 24 hours

// Log the request for debugging
$logFile = fopen("cors_debug_log.txt", "a");
fwrite($logFile, "Request received at " . date('Y-m-d H:i:s') . "\n");
fwrite($logFile, "Request method: " . $_SERVER['REQUEST_METHOD'] . "\n");
fwrite($logFile, "Request headers: " . json_encode(getallheaders()) . "\n\n");
fclose($logFile);

// Handle preflight OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// For other requests, return a simple response
$response = [
    "status" => "success",
    "message" => "CORS test successful",
    "timestamp" => date('Y-m-d H:i:s'),
    "request_method" => $_SERVER['REQUEST_METHOD']
];

header('Content-Type: application/json');
echo json_encode($response);
?>
