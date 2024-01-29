{ lib, pkgs, config, ... }:
with lib;
let
  cfg = config.services.fsr-print-interface;
  appEnv = pkgs.python311.withPackages (p: with p; [ gunicorn (pkgs.python311Packages.callPackage ./default.nix { }) ]);
in
{
  options.services.fsr-print-interface = {
    enable = mkEnableOption "";
    listenPort = mkOption {
      type = types.port;
      default = 8090;
      description = mdDoc ''
        Port the app will run on.
      '';
    };
    user = mkOption {
      type = types.str;
      default = "print-interface";
      description = "The user under which the server runs.";
    };
    group = mkOption {
      type = types.str;
      default = "print-interface";
      description = "The group under which the server runs.";
    };
    dataDir = mkOption {
      type = types.path;
      default = "/var/cache/print-interface";
      description = mdDoc ''
        The service's working directory
      '';
    };
    smtp = {
      username = mkOption {
        type = types.str;
        description = mdDoc ''
          SMTP username.
        '';
      };
      passwordFile = mkOption {
        type = types.path;
        default = null;
        description = mdDoc ''
          File containing the SMTP password. 
        '';
      };
    };
  };

  config = mkIf (cfg.enable) {
    systemd.tmpfiles.rules = [
      "d '${cfg.dataDir}' 0700 ${cfg.user} ${cfg.group} - -"
    ];
    systemd.services.fsr-print-interface = {
      enable = true;
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      environment = {
        PRINT_INTERFACE_USERNAME = cfg.smtp.username;
      };
      serviceConfig = {
        WorkingDirectory = cfg.dataDir;
        DynamicUser = true;
        LoadCredential = "print_interface_password:${cfg.smtp.passwordFile}";

        ExecStart = "${appEnv}/bin/gunicorn print_interface:app -b 0.0.0.0:${toString cfg.listenPort} --error-logfile -";
      };
    };
  };
}
