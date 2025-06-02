<?php
// CORS diagnostic file
// This file helps diagnose CORS issues

// Output all headers for debugging
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
header("Content-Type: application/json; charset=UTF-8");

// If OPTIONS request, return 200 OK
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Build response with diagnostic info
$response = array(
    'status' => 'success',
    'message' => 'CORS diagnostic response',
    'headers_received' => getallheaders(),
    'request_method' => $_SERVER['REQUEST_METHOD'],
    'request_uri' => $_SERVER['REQUEST_URI'],
    'server_info' => array(
        'software' => $_SERVER['SERVER_SOFTWARE'],
        'name' => $_SERVER['SERVER_NAME'],
        'port' => $_SERVER['SERVER_PORT'],
        'protocol' => $_SERVER['SERVER_PROTOCOL']
    )
);

// If POST data sent, include it in response
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = file_get_contents('php://input');
    $response['post_data_received'] = !empty($input);
    $response['post_data_type'] = gettype($input);
    $response['post_data_length'] = strlen($input);
    
    // Try to parse as JSON
    $json_data = json_decode($input, true);
    if ($json_data !== null) {
        $response['json_parse_success'] = true;
        // Include first few keys as confirmation
        $firstFew = array_slice($json_data, 0, 3, true);
        $response['json_sample'] = $firstFew;
    } else {
        $response['json_parse_success'] = false;
        $response['json_error'] = json_last_error_msg();
    }
}

// Send response
echo json_encode($response, JSON_PRETTY_PRINT);
