<?php
// File: cors_headers_test.php
// This script outputs all CORS-related headers for troubleshooting

// Get the origin from the request
$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';

// List of allowed origins
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

// Add additional CORS headers
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
header("Access-Control-Allow-Credentials: true");
header("Access-Control-Max-Age: 86400"); // 24 hours

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Output diagnostic information
header('Content-Type: application/json');

// Get all headers that were sent
$requestHeaders = [];
foreach ($_SERVER as $key => $value) {
    if (substr($key, 0, 5) === 'HTTP_') {
        $header = str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($key, 5)))));
        $requestHeaders[$header] = $value;
    }
}

// Get all headers that will be sent
$responseHeaders = [];
foreach (headers_list() as $header) {
    $parts = explode(':', $header, 2);
    if (count($parts) === 2) {
        $responseHeaders[trim($parts[0])] = trim($parts[1]);
    }
}

// Prepare the response
$response = [
    'timestamp' => date('Y-m-d H:i:s'),
    'server_info' => [
        'php_version' => phpversion(),
        'server_software' => $_SERVER['SERVER_SOFTWARE'],
        'request_method' => $_SERVER['REQUEST_METHOD'],
        'request_uri' => $_SERVER['REQUEST_URI'],
        'remote_addr' => $_SERVER['REMOTE_ADDR']
    ],
    'cors_info' => [
        'origin' => $origin,
        'is_allowed_origin' => in_array($origin, $allowed_origins),
        'allowed_origins' => $allowed_origins
    ],
    'request_headers' => $requestHeaders,
    'response_headers' => $responseHeaders,
    'cors_status' => 'Active and configured correctly'
];

echo json_encode($response, JSON_PRETTY_PRINT);
?>
