echo Hehe
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
docker build -t pauljohn28/webs .
cat ./password.txt | docker login --username pauljohn28 --password-stdin
docker push pauljohn28/webs

echo "Docker image built and pushed to docker hub !!"

kubectl apply -f ws.yaml
kubectl expose deployment webserdep --port=8000

echo "Please wait while the pod is being set up"

sleep 30

echo "All done !!"
echo "Use: curl app.192.168.49.2.nip.io/athlete to get my favourite athlete !!"