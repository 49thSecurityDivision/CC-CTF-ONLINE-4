import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';

void main() {
  runApp(const BackupApp());
}

class BackupApp extends StatelessWidget {
  const BackupApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Secure Cloud Backup',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const BackupHomePage(),
    );
  }
}

class BackupHomePage extends StatefulWidget {
  const BackupHomePage({Key? key}) : super(key: key);

  @override
  State<BackupHomePage> createState() => _BackupHomePageState();
}

class _BackupHomePageState extends State<BackupHomePage> {
  final List<FileUploadStatus> _uploadHistory = [];
  bool _isUploading = false;

  Future<void> _uploadFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['zip'],
    );

    if (result != null) {
      setState(() {
        _isUploading = true;
        _uploadHistory.insert(0, FileUploadStatus(
          filename: result.files.first.name,
          status: 'Uploading...',
          timestamp: DateTime.now(),
          progress: 0,
        ));
      });

      try {
        final file = File(result.files.first.path!);
        final request = http.MultipartRequest(
          'POST',
          Uri.parse('http://challenges.carolinacon.org:8016/upload'),
        );

        request.files.add(
          await http.MultipartFile.fromPath(
            'file',
            file.path,
            filename: result.files.first.name,
          ),
        );

        final response = await request.send();
        final responseData = await response.stream.bytesToString();
        final jsonResponse = json.decode(responseData);

        setState(() {
          _uploadHistory[0] = FileUploadStatus(
            filename: result.files.first.name,
            status: response.statusCode == 200 ? 'Success' : 'Failed',
            timestamp: DateTime.now(),
            progress: 100,
            message: jsonResponse['message'],
          );
        });
      } catch (e) {
        setState(() {
          _uploadHistory[0] = FileUploadStatus(
            filename: result.files.first.name,
            status: 'Error',
            timestamp: DateTime.now(),
            progress: 0,
            message: e.toString(),
          );
        });
      } finally {
        setState(() {
          _isUploading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Secure Cloud Backup'),
        elevation: 2,
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 4,
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Backup Files',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 8),
                Text(
                  'Upload your ZIP archives for secure cloud backup',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    ElevatedButton.icon(
                      onPressed: _isUploading ? null : _uploadFile,
                      icon: const Icon(Icons.upload_file),
                      label: const Text('Select ZIP File'),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _uploadHistory.length,
              padding: const EdgeInsets.all(16),
              itemBuilder: (context, index) {
                final upload = _uploadHistory[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: Icon(
                      upload.status == 'Success'
                          ? Icons.check_circle
                          : upload.status == 'Error'
                              ? Icons.error
                              : Icons.hourglass_bottom,
                      color: upload.status == 'Success'
                          ? Colors.green
                          : upload.status == 'Error'
                              ? Colors.red
                              : Colors.orange,
                    ),
                    title: Text(upload.filename),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '${upload.status} - ${_formatDate(upload.timestamp)}',
                        ),
                        if (upload.message != null)
                          Text(
                            upload.message!,
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        if (upload.status == 'Uploading...')
                          LinearProgressIndicator(value: upload.progress / 100),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.hour}:${date.minute.toString().padLeft(2, '0')} ${date.day}/${date.month}/${date.year}';
  }
}

class FileUploadStatus {
  final String filename;
  final String status;
  final DateTime timestamp;
  final double progress;
  final String? message;

  FileUploadStatus({
    required this.filename,
    required this.status,
    required this.timestamp,
    required this.progress,
    this.message,
  });
}
