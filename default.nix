{ buildPythonPackage, python311Packages, python, ... }:

buildPythonPackage {
  name = "print-interface";
  src = ./print_interface;

  propagatedBuildInputs = with python311Packages; [
    flask
    python-dotenv
    imaplib2
    gunicorn
  ];

  installPhase = ''
    runHook preInstall
    mkdir -p $out/${python.sitePackages}
    cp -r . $out/${python.sitePackages}/print_interface
    runHook postInstall '';

  shellHook = "export FLASK_APP=print_interface";

  format = "other";
}
