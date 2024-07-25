<?php
// Define some constants
define( "RECIPIENT_NAME", "ATRS Marketing" );
define( "RECIPIENT_EMAIL", "marketing@atrs1.com" );

// Read the form values
$success = false;
$userName = isset( $_POST['username'] ) ? preg_replace( "/[^\s\S\.\-\_\@a-zA-Z0-9]/", "", $_POST['username'] ) : "";
$senderEmail = isset( $_POST['email'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['email'] ) : "";
$senderPhone = isset( $_POST['phone'] ) ? preg_replace( "/[^\.\-\_\@a-zA-Z0-9]/", "", $_POST['phone'] ) : "";
$userSubject = isset( $_POST['subject'] ) ? preg_replace( "/[^\s\S\.\-\_\@a-zA-Z0-9]/", "", $_POST['subject'] ) : "";
$message = isset( $_POST['message'] ) ? preg_replace( "/(From:|To:|BCC:|CC:|Subject:|Content-Type:)/", "", $_POST['message'] ) : "";

// If all values exist, send the email
if ( $userName && $senderEmail && $message) {
  $recipient = RECIPIENT_NAME . " <" . RECIPIENT_EMAIL . ">";
  $headers = "From: " . $userName . " <" . $senderEmail . ">";
  $msgBody = "Name: ". $userName . "\nEmail: ". $senderEmail . "\nPhone: ". $senderPhone . "\nSubject: ". $userSubject . "\nMessage: " . $message;
  $success = mail( $recipient, $userSubject, $msgBody, $headers );

  //Set Location After Successful Submission
  header('Location: contact.html?message=Successfull');
} else {
  //Set Location After Unsuccessful Submission
  header('Location: contact.html?message=Failed');  
}
?>
