import json
import copy

class jsonDescription():

    num_device = 0


    def description(self, origin, temp):
        # update and append context information
        # print(self)

        #EdtectObject list preprocessing ## HJ 20210712
        listchek_list = temp['DetectObject']
        for i in listchek_list:
            if('/'in i):
                temp['DetectObject'][temp['DetectObject'].index(i)] = i.split('/')


        if not bool(origin):
            # print('append data')
            self.append(origin, temp)
        else :
            found = False
            number = 0
            id = temp['name'][0]
            for sub in origin:
                if sub['name'] == id:
                    # print("tempid :" , id, " origin id : " , sub['name'])
                    found = True
                    self.update(origin, temp, number)
                    break
                number=number+1

            if not found:
                # print('not found')
                self.append(origin, temp)

        with open('context.json', 'w', encoding="utf-8") as make_file:
            json.dump(origin, make_file, ensure_ascii=False, indent="\t")

        return origin

    def append(self, origin, temp):
        #append new work edgeserver context using arraylist
        # print('append data')
        
        
        data = {
            "name" : temp['name'][0],
            "Edgeserver" : {
                "netAddress" : temp['netAddress'][0],
                "CPU" : {
                    "cpuClock" : temp['cpuClock'][0],
                    "cpuUsage" : temp['cpuUsage'][0],
                    "cpuCore" : temp['cpuCore'][0],
                    "cpuOccupancy" : temp['cpuOccupancy'][0]
                },
                "RAM" : {
                    "totalMemory" : temp['totalMemory'][0],
                    "freeMemory" : temp['freeMemory'][0],
                    "memoryOccupancy" : temp['memoryOccupancy'][0]
                },
                "Storage" : {
                    "totalDisk" : temp['totalDisk'][0],
                    "freeDisk" : temp['freeDisk'][0],
                    "diskOccupancy" : temp['diskOccupancy'][0]
                },
                "connectedDevice" : temp['connectedDevice'][0]
            },
            "Device" : {
                "videoQuality" : temp['videoQuality'],
                "videoRate" : temp['videoRate'],
                "cameraIp" : temp['connectedDevice'],
                "deviceGPS" : {
                    "latitude" : temp['latitude'],
                    "longitude" : temp['longitude']
                },
                "Target" : temp['Target']
            },
            "AI": {
                "DetectObject": temp['DetectObject'],
                "RequiredResource": {
                    "CPU": temp['CPU'],
                    "RAM": temp['RAM']
                }
            }
        }
        origin.append(data)
        return origin

    def update(self, origin, temp, index):
        #
        # print(origin[index])
        # print(origin[index]['Edgeserver'])
        # print(index)
        origin[index]['Edgeserver']['CPU']['cpuClock'] = temp['cpuClock'][0]
        origin[index]['Edgeserver']['CPU']['cpuUsage'] = temp['cpuUsage'][0]
        origin[index]['Edgeserver']['CPU']['cpuOccupancy'] = temp['cpuOccupancy'][0]
        origin[index]['Edgeserver']['RAM']['freeMemory'] = temp['freeMemory'][0]
        origin[index]['Edgeserver']['RAM']['memoryOccupancy'] = temp['memoryOccupancy'][0]
        origin[index]['Edgeserver']['Storage']['diskOccupancy'] = temp['diskOccupancy'][0]
        origin[index]['Edgeserver']['Storage']['freeDisk'] = temp['freeDisk'][0]
        origin[index]['Edgeserver']['connectedDevice'] = temp['connectedDevice'][0]
        origin[index]['Device']['videoQuality'] = temp['videoQuality']
        origin[index]['Device']['videoRate'] = temp['videoRate']
        
        origin[index]['Device']['cameraIp'] = temp['connectedDevice']
        origin[index]['Device']['deviceGPS']['latitude'] = temp['latitude']
        origin[index]['Device']['deviceGPS']['longitude'] = temp['longitude']
        origin[index]['Device']['Target'] = temp['Target']
        
        origin[index]['AI']['DetectObject'] = temp['DetectObject']
        origin[index]['AI']['RequiredResource']['CPU'] = temp['CPU']
        origin[index]['AI']['RequiredResource']['RAM'] = temp['RAM']

        return origin

    def device_num_change_detector(self, temp):
        new_num_device = len(temp['Target'])
        print(new_num_device)
        print(self.num_device)
        if new_num_device != self.num_device:
            self.num_device = copy.deepcopy(new_num_device)
            # self.num_device = new_num_device
            print(self.num_device)
            return True
        else: 
            self.num_device = copy.deepcopy(new_num_device)
            # self.num_device = new_num_device
            print(self.num_device)
            return False

