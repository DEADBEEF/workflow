package edu.workflow.client;

import java.io.IOException;

import com.google.protobuf.ServiceException;

import edu.workflow.ping.PingPong.JobStatus;
import edu.workflow.ping.PingPong.JobStatusEnum;
import edu.workflow.ping.PingPong.StringMessage;

public class CheckJob {
	public static void run() throws IOException {
		ServerConnection connection =  new ServerConnection("AddJob");
		StringMessage jobId = StringMessage.newBuilder().setValue("Test Job").build();
		try {
			JobStatus status = connection.checkJobStatus(jobId);
			if (status.getStatus() == JobStatusEnum.NOTDONE) {
				System.out.print("BUSY");				
			} else if (status.getStatus() == JobStatusEnum.DONE) {
				System.out.print("DONE");
			} else {
				System.out.print("BUSY");
			}
		} catch (ServiceException e) {
			e.printStackTrace();
		} finally {
			connection.close();
		}
	}
}
