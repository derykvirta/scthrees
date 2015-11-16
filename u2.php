<?php

// configuration
$url = 'http://scthrees.com/admin2.html?p=asdf78901234jkl';
$file = 'data/l.txt';

// check if form has been submitted
if (isset($_POST['text']))
{
  // save the text contents
  file_put_contents($file, $_POST['text']);

  // redirect to form again
  header(sprintf('Location: %s', $url));
  printf('<a href="%s">Moved</a>.', htmlspecialchars($url));
  exit();
}

?>