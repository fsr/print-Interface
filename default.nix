{ buildPythonPackage, python311Packages, python, ... }:

buildPythonPackage {
  name = "print-interface";
  src = ./;

  propagatedBuildInputs = with python311Packages; [
    flask
    dotenv
  ];

  installPhase = ''
    runHook preInstall
    mkdir -p $out/${python.sitePackages}
    cp -r . $out/${python.sitePackages}/trucksimulatorbot-images
    runHook postInstall '';

  shellHook = "export FLASK_APP=print-interface";

  format = "other";
}