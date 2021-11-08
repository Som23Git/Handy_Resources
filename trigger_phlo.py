import plivo

auth_id = 'MANDLKMMMXZDKYZMVKNJ'
auth_token = 'ZDgzMmJmNWJhZTc0OGU4MTFhZmE5MjcxZDY5Nzcw'
phlo_id = 'b9487581-0f24-4521-bec7-1bd31ef3bb55' # https://console.plivo.com/phlo/list/
payload = {'from': '+16476970322','to':'+12142835956'}
phlo_client = plivo.phlo.RestClient(auth_id=auth_id, auth_token=auth_token)
phlo = phlo_client.phlo.get(phlo_id)
response = phlo.run(**payload)
print(response)

# import plivo

# auth_id = 'MANDLKMMMXZDKYZMVKNJ'
# auth_token = 'ZDgzMmJmNWJhZTc0OGU4MTFhZmE5MjcxZDY5Nzcw'
# phlo_id = 'b9487581-0f24-4521-bec7-1bd31ef3bb55' # https://console.plivo.com/phlo/list/
# phlo_client = plivo.phlo.RestClient(auth_id=auth_id, auth_token=auth_token)
# phlo = phlo_client.phlo.get(phlo_id)
# response = phlo.run()
# # print str(response)

