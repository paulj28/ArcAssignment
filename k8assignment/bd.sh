echo "Beginning the Build & Deploy Script ..."
python3 -m server.py &
pid=$!

sleep 1

pi=$(lsof -t -i:8000)

echo "Process id = ${pi}"

val=$(python3 -m tester)

echo "Value of val = ${val}"
act="True"
kill -9 "${pid}"

if [[ "$val" != "$act" ]] ; then
exit 1
fi

echo "Test Passed !!"

echo "Setting up Minikube !"

minikube start

minikube addons enable ingress

kubectl delete validatingwebhookconfigurations ingress-nginx-admission

eval $(minikube -p minikube docker-env)

echo "Minikube setup complete !"

echo "Building docker image !"

docker build -t arcassignment/ws .

echo "Docker image built !"

echo "Beginning deployment !"

kubectl apply -f ws.yaml
kubectl expose deployment webserdep --port=8000

echo "Please wait while everything is being set up ..."

sleep 30

echo "All done !!"
echo "Verify Ingress IP has been set before checking. Use: kubectl get ingress"
echo "Use: curl app.192.168.49.2.nip.io/athlete to get my favourite athlete !!"
