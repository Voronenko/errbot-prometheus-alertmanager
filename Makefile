codegen-get:
	wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.2/swagger-codegen-cli-2.4.2.jar -O swagger-codegen-cli.jar

codegen-help:
	java -jar swagger-codegen-cli.jar help

alertmanager-api-refresh:
	wget https://raw.githubusercontent.com/prometheus/alertmanager/master/api/v2/openapi.yaml -O openapi.yaml

alertmanager-client-stub:
	java -jar swagger-codegen-cli.jar generate -i openapi.yaml -l python -o alertmanager
